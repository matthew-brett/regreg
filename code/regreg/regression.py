#this is brad's  branch
import numpy as np

class Regression(object):

    def __init__(self, problem):
        self.problem = problem

    @property
    def output(self):
        """
        Return the 'interesting' part of the problem arguments.
        In the regression case, this is the tuple (beta, r).
        """
        return self.problem.output

    def fit(self):
        """
        Abstract method.
        """
        raise NotImplementedError

class ISTA(Regression):

    debug = False
    def fit(self,L,tol=1e-4,max_its=100,min_its=5):

        itercount = 0
        obj_cur = np.inf
        while itercount < max_its:
            f_beta = self.problem.obj(self.problem.coefs)
            grad = self.problem.grad(self.problem.coefs)
            self.problem.coefs = self.problem.proximal(self.problem.coefs, grad, L)
            obj = self.problem.obj(self.problem.coefs)
            if np.fabs((obj_cur - f_beta) / f_beta) < tol and itercount >= miniter:
                break
            itercount += 1
        if self.debug:
            print "ISTA used", itercount, "iterations"

class FISTA(Regression):

    debug = False
    # XXX move L to self.problem...
    def fit(self,L,max_its=100,tol=1e-5,miniter=5):

        f = self.problem.obj
        
        r = self.problem.coefs
        t_old = 1.
        
        obj_cur = np.inf
        itercount = 0
        while itercount < max_its:
            f_beta = f(self.problem.coefs)
            if np.fabs((obj_cur - f_beta) / f_beta) < tol and itercount >= miniter:
                break
            obj_cur = f_beta
                    
            grad =  self.problem.grad(r)
            beta = self.problem.proximal(r, grad, L)

            t_new = 0.5 * (1 + np.sqrt(1+4*(t_old**2)))
            r = beta + ((t_old-1)/(t_new)) * (beta - self.problem.coefs)
            self.problem.coefs = beta
            t_old = t_new
            itercount += 1

        if self.debug:
            print "FISTA used", itercount, "iterations"
    
class NesterovSmooth(Regression):
    
    def fit(self,L,tol=1e-4,epsilon=0.1,max_its=100):
        import nesterov_smooth
        p = len(self.problem.coefs)
        grad_s, L_s, f_s = self.problem.smooth(L, epsilon)
        self.problem.coefs, l = nesterov_smooth.loop(self.problem.coefs, grad_s, L_s, f=f_s, maxiter=max_its, values=True, tol=tol)
        return f_s


import subfunctions as sf
class CWPath(Regression):

    debug = False
    def __init__(self, problem, **kwargs):
        self.problem = problem
            
    def fit(self,tol=1e-4,inner_its=50,max_its=2000,min_its=5):
        
        active = np.arange(self.problem.coefs.shape[0])
        itercount = 0
        stop = False
        while not stop and itercount < max_its:
            bold = self.output
            nonzero = []
            self.problem.update_cwpath(active,nonzero,1,update_nonzero=True)
            if itercount > min_its:
                stop, worst = self.stop(bold,tol=tol,return_worst=True)
                if np.mod(itercount,40)==0 and self.debug:
                    print "Fit iteration", itercount, "with max. relative change", worst
            self.problem.update_cwpath(np.unique(nonzero),nonzero,inner_its)
            itercount += 1

    def stop(self,
             previous,
             tol=1e-4,
             return_worst = False):
        """
        Convergence check: check whether 
        residuals have not significantly changed or
        they are small enough.

        Both old and current are expected to be (beta, r) tuples, i.e.
        regression coefficent and residual tuples.
    
        """

        bold, _ = previous
        bcurrent, _ = self.output

        if return_worst:
            status, worst = sf.coefficientCheckVal(bold, bcurrent, tol)
            if status:
                return True, worst
            return False, worst
        else:
            status = sf.coefficientCheck(bold, bcurrent, tol)
            if status:
                return True
            return False

class Direct(Regression):
    #XXX for PMD problems
    def fit(self,tol=1e-4):
        self.problem.update_direct()