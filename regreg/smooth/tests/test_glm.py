import numpy as np
import nose.tools as nt

from regreg.smooth.glm import glm

def test_logistic():

    for Y, T in [(np.random.binomial(1,0.5,size=(10,)),
                  np.ones(10)),
                 (np.random.binomial(1,0.5,size=(10,)),
                  None),
                 (np.random.binomial(3,0.5,size=(10,)),
                  3*np.ones(10))]:
        X = np.random.standard_normal((10,5))

        L = glm.logistic(X, Y, trials=T)
        L.smooth_objective(np.zeros(L.shape), 'both')

        if T is None:
            np.testing.assert_allclose(L.gradient(np.zeros(L.shape)),
                                       X.T.dot(0.5 - Y))
            np.testing.assert_allclose(L.hessian(np.zeros(L.shape)),
                                       X.T.dot(X) / 4.)
        else:
            L.gradient(np.zeros(L.shape))
            L.hessian(np.zeros(L.shape))

        L.objective(np.zeros(L.shape))
        L.latexify()

        L.loss.data = (Y, T)
        L.loss.data

        L.data = (X, (Y, T))
        L.data

def test_poisson():

    X = np.random.standard_normal((10,5))
    Y = np.random.poisson(10, size=(10,))

    L = glm.poisson(X, Y)
    L.smooth_objective(np.zeros(L.shape), 'both')

    np.testing.assert_allclose(L.gradient(np.zeros(L.shape)),
                               X.T.dot(1 - Y))
    np.testing.assert_allclose(L.hessian(np.zeros(L.shape)),
                               X.T.dot(X))

    L.objective(np.zeros(L.shape))
    L.latexify()

    L.loss.data = Y
    L.loss.data

    L.data = (X, Y)
    L.data

def test_gaussian():

    X = np.random.standard_normal((10,5))
    Y = np.random.standard_normal(10)

    L = glm.gaussian(X, Y)
    L.smooth_objective(np.zeros(L.shape), 'both')

    np.testing.assert_allclose(L.gradient(np.zeros(L.shape)),
                               -X.T.dot(Y))
    np.testing.assert_allclose(L.hessian(np.zeros(L.shape)),
                               X.T.dot(X))

    L.objective(np.zeros(L.shape))
    L.latexify()

    L.loss.data = Y
    L.loss.data

    L.data = (X, Y)
    L.data

def test_huber():

    X = np.random.standard_normal((10,5))
    Y = np.random.standard_normal(10)

    L = glm.huber(X, Y, 0.1)
    L.smooth_objective(np.zeros(L.shape), 'both')

    L.gradient(np.zeros(L.shape))
    nt.assert_raises(NotImplementedError, L.hessian, np.zeros(L.shape))

    L.objective(np.zeros(L.shape))
    L.latexify()

    L.loss.data = Y
    L.loss.data

    L.data = (X, Y)
    L.data

