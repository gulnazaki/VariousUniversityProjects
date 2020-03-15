function out = alt_Box_Filt_Hessian(img, s)

% Calculate a box-filter approximation of Hessian
%     img = imread('Caravaggio2.jpg');
%     s = 1;
    if ndims(img) == 3
        img = rgb2gray(img);
    end
    FiltDxx = alt_mask( s, 'Dxx');
    FiltDyy = alt_mask( s, 'Dyy');
    FiltDxy = alt_mask( s, 'Dxy');
%     intImg = cumsum( img ) ;
%     intImg = cumsum(intImg,2);
%     intImg = img;
%     Lxx = imfilter(intImg, FiltDxx);
%     Lyy = imfilter(intImg, FiltDyy);
%     Lxy = imfilter(intImg, FiltDxy);
    
    intImg = integralImage(img);
    Lxx = integralFilter (intImg, FiltDxx);
    Lyy = integralFilter(intImg, FiltDyy);
    Lxy = integralFilter(intImg, FiltDxy);
    out = Lxx + Lyy - 0.9 * Lxy.^2;
    size = FiltDxx.Size;
    out = padarray(out,floor(size/2) , 0, 'symmetric');
%     out = out(2:end ,2:end);    
end