function multiscale_blob_detect (img, N, sigma)
    
    img_ = rgb2gray(img);
    s = 1.5;
    s_scale_array = sigma*s.^(0:N-1);

    pixmap1 = blob_detect(img_,s_scale_array(1));
    lap_m1 = laplacian_metric(pixmap1, s_scale_array(1));
    pixmap2 = blob_detect(img_,s_scale_array(2));
    lap_m2 = laplacian_metric(pixmap2, s_scale_array(2));
    pixmap3 = blob_detect(img_,s_scale_array(3));
    lap_m3 = laplacian_metric(pixmap3, s_scale_array(3));

    keep0 = (pixmap2>=pixmap1 & pixmap2>=pixmap3); 

    img_size = size(img_);
    height = img_size(1);
    width = img_size(2);
    point_scale_matrix = zeros (img_size(1), img_size(2));
    for idx = 1:N
        if idx<4
        pixmap1 = blob_detect(img_,s_scale_array(1));
        lap_m1 = laplacian_metric(pixmap1, s_scale_array(1));
        pixmap2 = blob_detect(img_,s_scale_array(2));
        lap_m2 = laplacian_metric(pixmap2, s_scale_array(2));
        pixmap3 = blob_detect(img_,s_scale_array(3));
        lap_m3 = laplacian_metric(pixmap3, s_scale_array(3));
        keep0 =   ( ((lap_m2>=lap_m1) & (lap_m2>=lap_m3)) & pixmap2 ); 
        point_scale_matrix = point_scale_matrix + (keep0 & (point_scale_matrix==0)) * sigma ;

        else
            pixmap1 = pixmap2;
            lap_m1 = lap_m2;
            pixmap2 = pixmap3;
            lap_m2 = lap_m3;
            sigma = s_scale_array(idx) ;
            pixmap3 =  blob_detect(img_,sigma );
            lap_m3 = laplacian_metric(pixmap3, sigma );    
            keep1 =   ( ((lap_m2>=lap_m1) & (lap_m2>=lap_m3)) & pixmap2 ); 
            point_scale_matrix = point_scale_matrix + (keep1 & (point_scale_matrix==0)) * sigma ;
        end
    end
    [row, col, value] = find(point_scale_matrix);
    interest_points_visualization(img, [col, row, value]);
end
