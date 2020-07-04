from Matrix import matrix

def kalman_filter(x, u, P, F, R, H, z):

    I = matrix([[]])
    I = I.identity(x.dimx)
    
    #measurement update
    y = z-H*x
    S = H*P*H.transpose()+R
    K = P*H.transpose()*S.inverse()
    x = x + K*y
    P = (I-K*H)*P
    #prediction
    x = F*x + u;
    P = F*P*F.transpose()
        
    return x,P

def main():
    
    measurements = [[[1.0],[2.0]],
                    [[2.0],[4.0]],
                    [[3.0],[6.0]]]

    
    x = matrix([[0.],
                [0.],
                [0.],
                [0.]])

    u = matrix([[]])
    u = u.zero(x.dimx, x.dimy)
    
    P = matrix([[50., 0., 0., 0.],
                [0., 50., 0., 0.],
                [0., 0., 50., 0.],
                [0., 0., 0., 50.]]) # initial uncertainty
    
    F = matrix([[1., 1., 0., 0.],
                [0., 1., 0., 0.],
                [0., 0., 1., 1.],
                [0., 0., 0., 1.]]) # next state function
    H = matrix([[1., 0., 0., 0.],
                [0., 0., 1., 0.]]) # measurement function
    
    R = matrix([[1., 0.],
                [0., 1.]]) # measurement uncertainty

    for i in range(len(measurements)):
        z = matrix(measurements[i])
        x, P = kalman_filter(x, u, P, F, R, H, z)
        
    print(x)

if __name__ == "__main__":
    main()