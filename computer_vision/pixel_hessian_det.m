function out = pixel_hessian_det(img_)
%     img = im2double(img_);
%     gauss_dim = ceil( 3 * sigma)*2 + 1 ;
%     gaussian = fspecial('gaussian', gauss_dim, sigma);
%     img = imfilter(img, gaussian, 'symmetric');

    [Lx, Ly] = gradient(img_);
    [Lxx, Lxy] = gradient(Lx);
    [Lyx, Lyy] = gradient(Ly);
    determinant = Lxx.*Lyy - Lxy.^2;        %condition1

    out = determinant;

end