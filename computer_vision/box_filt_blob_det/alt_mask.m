function out = alt_mask(s, name)    
    n = ceil( s * 3) * 2 + 1;
    if (strcmp( name , 'Dxx') || strcmp (name, 'Dyy'))
        h = 4*floor(n/6) + 1;
        w = 2*floor(n/6) + 1;
        h_start = (n - h) / 2 + 1;
        h_fin = h_start + h  - 1 ;
        %% Positve windows
        Pos_window_centers = ceil((1:2:3)/4 * n);
        P_Lefts = Pos_window_centers - floor(w/2) ;
        P_Rights = Pos_window_centers + floor(w/2) ;
        %% Negative windows    
        Neg_window_center = ceil(n/2);
        Neg_Lefts = Neg_window_center - floor(w/2) ;
        Neg_Rights = Neg_window_center + floor(w/2);
        
        %% Create Integral Kernel
        marg1X = 1;
        marg1Y = h_fin + 1;
        margH = (n-h)/2;
        margW = n;
        if strcmp( name,'Dxx')
            out = integralKernel([P_Lefts(1), h_start, w, h; P_Lefts(2),h_start,w,h; marg1X, marg1Y, margW, margH; Neg_Lefts(1), h_start, w, h], [1, 1, 0 , -2])   ;

        %% Just rotate for Dyy
        elseif strcmp(name, 'Dyy')
            out = integralKernel([ h_start, P_Lefts(1), h, w; h_start,P_Lefts(2), h, w; marg1Y,marg1X, margH, margW; h_start,Neg_Lefts(1), h, w], [1, 1, 0 , -2])   ;

        end
    elseif strcmp(name, 'Dxy') || strcmp(name,'Dyx')
        m = 2* floor( n/6) + 1;
        centers = ceil(( 1 :2: 3) * n/4);

        Lefts = centers - floor(m/2);
        Rights = centers + floor(m/2);
        Ups = centers - floor(m/2);
        Downs = centers + floor(m/2);
        %% Create Integral Kernel
        marg1X = max(Rights)+ 1;
        marg1Y = 1;
        marg1H = n;
        marg1W = Lefts(1) - 1;
        
        marg2X = marg1X;
        marg2Y = marg1X;
        marg2H = marg1H;
        marg2W = marg1W;
        if n - max(Rights) == 0
            out = integralKernel([Lefts(1),Ups(1),m,m; Lefts(2),Ups(2),m,m;Lefts(1),Ups(2),m,m; Lefts(2),Ups(1),m, m],[1,1,-1,-1]);
        else
            out = integralKernel([Lefts(1),Ups(1),m,m; Lefts(2),Ups(2),m,m;Lefts(1),Ups(2),m,m; Lefts(2),Ups(1),m, m; marg1X, marg1Y, marg1W, marg1H],[1,1,-1,-1,0]);
        end
    end
    
end
