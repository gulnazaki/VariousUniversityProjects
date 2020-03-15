function s_points = blob_detect(img,sigma)
    %Blob detection with the use of the Hessian operator
    ns = ceil(sigma*3)*2+1;
    %% Use of Hessian
    img = imfilter (img, fspecial('gaussian',ns,sigma));
    R = pixel_hessian_det(img) ;

    %% Various Criteria
    ns = ceil(3*sigma)*2+1;
    B_sq = strel('disk',ns);
    Cond1 = ( R == imdilate(R,B_sq) );
    % figures
    % figure(2)
    % subplot(2,2,1)
    % imshow(imdilate(R,B_sq))
    % subplot(2,2,2)
    % imshow(Cond1)
    threshold = 0.01 * max ( R (:));
    Cond2 = ( R > threshold);
    s_points = Cond1 & Cond2;
    
    % s_points = s_points .* R ; 
    % s_points = find_local_maxima(determ,sigma);
    % [pointY, pointX] = find(s_points);
    % points = [pointY, pointX];
    % point_sigma_array = [points, sigma * ones(size(pointY))];
end
