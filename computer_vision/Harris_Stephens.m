function out =  Harris_Stephens( varargin )
%Harris_Stephens function applies the Harris Sthephens corner detection
%algorithm to given img image, with a differentiation scale s and
%integretion scale r
    if nargin == 5
    %     img_ ,s, r, theta;
        img = varargin{1};
        s = varargin{2};
        r = varargin{3};
        theta = varargin{4};
        multi = varargin{5};
    elseif nargin == 1 
        img = varargin{1};
        theta = 0.005;
        s = 2;
        r = 2.5;
        multi = 0;
    end

    ns = ceil(3*s)*2 + 1;
    nr = ceil(3*r)*2 + 1;

    Gr = fspecial('gaussian', nr, r);
    Gs = fspecial('gaussian', ns, s);
    img_g = imfilter (img, Gs);
    [Ix, Iy] = gradient(img_g);
    IxIx = Ix.*Ix ;
    IxIy = Ix.*Iy ;
    IyIy = Iy.*Iy ;
    J1 = imfilter(IxIx, Gr);
    J2 = imfilter(IxIy, Gr);
    J3 = imfilter(IyIy, Gr);

    %% Eigenvalues
    par1 = 1/2*(J1 +J3);
    par2 = 1/2*sqrt( (J1 - J3).^2 + 4*J2.^2 );

    lambda_plus = par1 + par2 ;
    %imshow(lambda_plus,[]);
    %pause
    lambda_minus = par1 - par2 ;
    %imshow(lambda_minus,[]);
    %pause
    %% Cornerness Criterion
    % k = positive_float_value;
    k = 0.05;
    R = lambda_plus.*lambda_minus - k * (lambda_minus.*lambda_plus).^2;
    % Conditions
    % 1
    B_sq = strel('disk', ns);
    Cond1 = (R == imdilate(R, B_sq) );
    % 2
    Cond2 = (R > max(R(:)) * theta );
    pix_map = img.*(Cond1 & Cond2) ;
    if multi == 0
        [pointX, pointY] = find(pix_map) ;
        out = [pointY pointX s*ones(1, max(size(pointX)))' ];
    else
        out = pix_map;
    end
end

