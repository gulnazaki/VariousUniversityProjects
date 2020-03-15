function out = alt_multiscale_blob_detect ( img_, N)
    if ndims(img_) == 3
        img = rgb2gray(img_);
    else
        img = img_;
    end
    
    sigma = 2;
    s = 1.5;
    points= alt_blob_detect( img,sigma );
%     N = 6;
    s_array = sigma*s.^(0:N-1);

    pixmap1 = alt_blob_detect(img,s_array(1));
    lap_m1 = laplacian_metric(img, s_array(1));
    pixmap2 = alt_blob_detect(img,s_array(2));
    lap_m2 = laplacian_metric(img, s_array(2));
    pixmap3 = alt_blob_detect(img,s_array(3));
    lap_m3 = laplacian_metric(img, s_array(3));

    keep0 = ((lap_m2>=lap_m1 & lap_m2>=lap_m3 )& pixmap2); 
    pixmap3 = pixmap3 & not ((lap_m2>=lap_m1 & lap_m2>=lap_m3 )& pixmap2);

    img_size = size(img);
    height = img_size(1);
    width = img_size(2);
    point_scale_matrix = zeros (img_size(1), img_size(2)); 
    for idx = 1:N
        if idx<4
        pixmap1 = alt_blob_detect(img,s_array(1));
        lap_m1 = laplacian_metric(img, s_array(1));

        pixmap2 =alt_blob_detect(img,s_array(2));
        lap_m2 = laplacian_metric(img, s_array(2));

        pixmap3 = alt_blob_detect(img,s_array(3));
        lap_m3 = laplacian_metric(img, s_array(3));
        keep0 =   ( ((lap_m2>=lap_m1) & (lap_m2>=lap_m3)) & pixmap2 ); 

        point_scale_matrix = point_scale_matrix + (keep0 & (point_scale_matrix==0)) * sigma ;
        pixmap3 = pixmap3 & not ((lap_m2>=lap_m1 & lap_m2>=lap_m3 )& pixmap2);

        else
            idx
            pixmap1 = pixmap2;
            lap_m1 = lap_m2;
            pixmap2 = pixmap3;
            lap_m2 = lap_m3;
            sigma = s_array(idx) ;
            pixmap3 =  alt_blob_detect(img,sigma );
            lap_m3 = laplacian_metric(img, sigma );

            lap_m3 = imdilate( lap_m3, strel('disk', ceil( 3* s_array(idx))*2 +1));

            keep1 =   ( ((lap_m2>=lap_m1) & (lap_m2>=lap_m3)) & pixmap2 );
            point_scale_matrix = point_scale_matrix + (keep1 & (point_scale_matrix==0)) * sigma ;
            pixmap3 = pixmap3 & not ((lap_m2>=lap_m1 & lap_m2>=lap_m3 )& pixmap2);

        end
    end
    
    [row, col, value] = find(point_scale_matrix);
    out = [row, col, value] ;
% interest_points_visualization(img_ , [col, row, value]);
end
