function out = find_local_maxima (img, sigma)
    ns = ceil(3* sigma)* 2 + 1;
    Gs = fspecial( 'gaussian', ns, sigma);
    
    [Ix, Iy] = gradient(img);
    IxIx = Ix.*Ix ;
    IxIy = Ix.*Iy ;
    IyIy = Iy.*Iy ;
    J1 = imfilter(IxIx, Gs);
    J2 = imfilter(IxIy, Gs);
    J3 = imfilter(IyIy, Gs);
    J = [J1, J2, J3];

    par1 = 1/2*(J1 +J3);
    par2 = 1/2*sqrt( (J1 - J3).^2 + 4*J2.^2 );

    lambda_plus = par1 + par2 ;
    lambda_minus = par1 - par2 ;
    k = 0.05;
    R = lambda_plus.*lambda_minus - k * (lambda_minus.*lambda_plus).^2;

    ns = ceil(3* sigma)* 2 + 1;
    B_sq = strel('disk', ns);
    
    maxima = ( R == imdilate( R, B_sq));
    out = maxima ;
end
