function s_points = alt_blob_detect(img,sigma)
    %Blob detection with the use of the Hessian operator
    img_ = im2double(img);
    % img_ = rgb2gray(img_);
    ns = ceil(sigma*3)*2+1;
    %% Use of box filters
    R = alt_Box_Filt_Hessian( img_ , sigma);
    
    imshow(R)
    %% Various Criteria
    ns = ceil(3*sigma)*2+1;
    B_sq = strel('disk',ns);
    Cond1 = ( R == imdilate(R,B_sq) );

    threshold = 0.32* max ( R (:));
    Cond2 = ( R > threshold);
    s_points = Cond1 & Cond2;
    

end
