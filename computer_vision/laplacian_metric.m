function out = laplacian_metric ( Matrix, sigma )
    ns = ceil( 3* sigma) * 2 + 1;
    log_filter = fspecial ( 'log', ns, sigma);
    lapl_of_matrix = imfilter(Matrix, log_filter, 'symmetric');
    out = (sigma^2) *abs ( lapl_of_matrix); 
end