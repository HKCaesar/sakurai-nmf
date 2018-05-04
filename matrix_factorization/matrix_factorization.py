"""Interface of semi-NMF and Nonlinear semi-NMF"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools
import numpy as np
import tensorflow as tf

BATCH_FIRST = True


def semi_nmf(a, u, v,
             use_bias=False,
             use_tf=False,
             data_format=BATCH_FIRST,
             num_iters=1,
             rcond=1e-14,
             eps=1e-15,
             alpha=1e-2,
             beta=1e-2):
    """Semi-NMF
    Args:
        a: Original matrix factorized
        u: Left matrix
        v: Non-negative matrix
        data_format: if BATCH_FIRST, a's shape should be [batch_size, input_size]
        use_bias: Use bias
        use_tf: When use Tensorflow, `a` should be instance of tf.placeholder
        num_iters: Number of iterations
        rcond: Reciprocal condition number
        eps:
        alpha: Coefficient for solve u.
        beta: Coefficient for solve v.

    Returns:
        When use TensorFlow, it returns operation u and v solved.
        When use NumPy, it returns results of u and v.
    """
    
    if use_bias:
        from matrix_factorization.np_biased_nmf import semi_nmf as semi_nmf_
        _semi_nmf = functools.partial(semi_nmf_,
                                      alpha=alpha,
                                      beta=beta,
                                      rcond=rcond,
                                      eps=eps,
                                      num_iters=num_iters,
                                      )
    else:
        from matrix_factorization.np_nmf import semi_nmf as semi_nmf_
        _semi_nmf = functools.partial(semi_nmf_,
                                      rcond=rcond,
                                      eps=eps,
                                      num_iters=num_iters,
                                      )
    
    if isinstance(a, np.ndarray) and not use_tf:
        # The algorithm is implemented as MATLAB format.
        # So that we have to transpose the matricies.
        if data_format is BATCH_FIRST:
            u_t, v_t = _semi_nmf(a=a.T, u=v.T, v=u.T)
            u = v_t.T
            v = u_t.T
            return u, v
        # For MATLAB format.
        return _semi_nmf(a=a, u=u, v=v)
    
    if use_tf:
        # For using tf.py_func the shape of matrix will be <unknown>
        u_shape = u.shape
        v_shape = v.shape
        if data_format is BATCH_FIRST:
            a_t = tf.transpose(a)
            tf_u_t, tf_v_t = tf.py_func(_semi_nmf,
                                        [a_t, tf.transpose(v), tf.transpose(u)],
                                        [tf.float64, tf.float64])
            tf_u = tf.check_numerics(tf.transpose(tf_v_t), 'u')
            tf_v = tf.check_numerics(tf.transpose(tf_u_t), 'v')
            tf_u.set_shape(u_shape)
            tf_v.set_shape(v_shape)
            return tf_u, tf_v
        tf_u, tf_v = tf.py_func(_semi_nmf, [a, u, v], [tf.float64, tf.float64])
        tf_u = tf.check_numerics(tf_u, 'u')
        tf_v = tf.check_numerics(tf_v, 'v')
        tf_u.set_shape(u_shape)
        tf_v.set_shape(v_shape)
        return tf_u, tf_v
    
    raise NotImplementedError('Never implement other type matrix')


def nonlin_semi_nmf(a, u, v,
                    use_bias=False,
                    use_tf=False,
                    data_format=BATCH_FIRST,
                    num_iters=1,
                    num_calc_u=1,
                    num_calc_v=1,
                    rcond=1e-14,
                    eps=1e-15,
                    alpha=1e-2,
                    beta=1e-2):
    """Nonlinear Semi-NMF
    Args:
        a: Original matrix factorized
        u: Left matrix
        v: Non-negative matrix
        use_bias: Use bias
        use_tf: When use Tensorflow, `a` should be instance of tf.placeholder
        data_format: if BATCH_FIRST, a's shape should be [batch_size, input_size]
        num_iters: Number of iterations
        rcond: Reciprocal condition number
        num_calc_u: Number of calculating u.
        num_calc_v: Number of calculating v.
        eps:
        alpha: Coefficient for solve u.
        beta: Coefficient for solve v.

    Returns:
        When use TensorFlow, it returns operation u and v solved.
        When use NumPy, it returns results of u and v.
    """
    if use_bias:
        from matrix_factorization.np_biased_nmf import nonlin_semi_nmf as nonlin_semi_nmf_
        _nonlin_semi_nmf = functools.partial(nonlin_semi_nmf_,
                                             alpha=alpha,
                                             beta=beta,
                                             rcond=rcond,
                                             eps=eps,
                                             num_iters=num_iters,
                                             num_calc_u=num_calc_u,
                                             num_calc_v=num_calc_v,
                                             )
    else:
        from matrix_factorization.np_nmf import nonlin_semi_nmf as nonlin_semi_nmf_
        _nonlin_semi_nmf = functools.partial(nonlin_semi_nmf_,
                                             rcond=rcond,
                                             eps=eps,
                                             num_iters=num_iters,
                                             num_calc_u=num_calc_u,
                                             num_calc_v=num_calc_v,
                                             )
    
    if isinstance(a, np.ndarray) and not use_tf:
        # The algorithm is implemented as MATLAB format.
        # So that we have to transpose the matricies.
        if data_format is BATCH_FIRST:
            u_t, v_t = _nonlin_semi_nmf(a=a.T, u=v.T, v=u.T)
            u = v_t.T
            v = u_t.T
            return u, v
        # For MATLAB format.
        return _nonlin_semi_nmf(a=a, u=u, v=v)
    
    if use_tf:
        # For using tf.py_func the shape of matrix will be <unknown>
        u_shape = u.shape
        v_shape = v.shape
        if data_format is BATCH_FIRST:
            a_t = tf.transpose(a)
            u_t = tf.transpose(u)
            v_t = tf.transpose(v)
            tf_u_t, tf_v_t = tf.py_func(_nonlin_semi_nmf, [a_t, v_t, u_t], [tf.float64, tf.float64])
            tf_u = tf.check_numerics(tf.transpose(tf_v_t), 'u')
            tf_v = tf.check_numerics(tf.transpose(tf_u_t), 'v')
            tf_u.set_shape(u_shape)
            tf_v.set_shape(v_shape)
            return tf_u, tf_v
        # For MATLAB format.
        tf_u, tf_v = tf.py_func(_nonlin_semi_nmf, [a, u, v], [tf.float64, tf.float64])
        tf_u = tf.check_numerics(tf_u, 'u')
        tf_v = tf.check_numerics(tf_v, 'v')
        tf_u.set_shape(u_shape)
        tf_v.set_shape(v_shape)
        return tf_u, tf_v
    
    raise NotImplementedError('Never implement other type matrix')