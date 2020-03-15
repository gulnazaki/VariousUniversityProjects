I1 = imread('sunflowers18.png');
I1 = rgb2gray(I1);
I1 = im2double(I1);
I2 = imread('Caravaggio2.jpg');
I2 = rgb2gray(I2);
I2 = im2double(I2);
IntI1 = integralImage(I1);
IntI2 = integralImage(I2);
% A = IntIm(2:end , 2:end);
% B = cumsum(img);
% B = cumsum(B,2);

imshow(IntI1,[]);
pause
imshow(IntI2,[]);
pause

s = 0.7;
%% Create masks
function out = operator(s, name)

    if strcmp( name , 'Dxx') | strcmp (name, 'Dyy')
        n = ceil(s * 3) * 2 + 1;

        h = 4*floor(n/6) + 1;
        w = 2*floor(n/6) + 1;

        Dxx = zeros(n+2);

        h_start = (n - h)/2 - 1;
        h_fin = h_start + h + 1;
        %% Positve windows
        Pos_window_centers = ceil((1:2:3)/4 * 7)';
        P_Lefts = Pos_window_centers - floor(w/2) - 1;
        P_Rights = Pos_window_centers + floor(w/2) ;
        Pos_positives = [h_start P_Lefts(1); h_start P_Lefts(2); h_fin P_Rights(1); h_fin P_Rights(2)];
        Pos_negatives = [h_fin P_Lefts(1) ; h_fin P_Lefts(2); h_start  P_Rights(1); h_start P_Rights(2)];
        % Dxx(hs:h+hs-1,:) = 1;
        %% Negative windows    
        Neg_window_center = ceil(7/2);
        Neg_horizontal_bord = [Neg_window_center - floor(w/2), Neg_window_center + floor(w/2) ];
        Neg_Lefts = Neg_window_center - floor(w/2);
        Neg_Rights = Neg_window_center + floor(w/2);

        Neg_positives = [h_start Neg_Lefts(1); h_fin Neg_Rights(1)];
        Neg_negatives = [h_fin Neg_Lefts(1) ; h_start  Neg_Rights(1)];
        %% Define the filters
        Pos_positves = Pos_positives+1;
        Pos_negatives = Neg_negatives+1;
        Neg_positives = Neg_positives+1;
        Neg_negatives = Neg_negatives+1;    
        
        Mask = zeros(n+2);
        PosposIdx = sub2ind( size(Mask), Pos_positives(:,1), Pos_positives(:,2));
        PosnegIdx = sub2ind( size(Mask), Pos_negatives(:,1), Pos_negatives(:,2));
        NegposIdx = sub2ind( size(Mask), Neg_positives(:,1), Neg_positives(:,2));
        NegnegIdx = sub2ind( size(Mask), Neg_negatives(:,1), Neg_negatives(:,2));
        %% Final
        mask = zeros( n+ 2);
        mask (PosposIdx) = 1;
        Mask = Mask + mask ;

        mask = 0* mask;
        mask (PosnegIdx) = -1;
        Mask = Mask + mask ;
        %
        mask = 0*mask;
        mask (NegposIdx) = -2;
        Mask = Mask + mask ;

        mask = (0*mask);
        mask (NegnegIdx) = 2;
        Mask = Mask + mask ;
%% Just rotate for Dyy
        if strcmp(name, 'Dyy')
        Dyy = Dxx';
        Mask = Dyy;
        end
        out = Mask;
    elseif strcmp(name, 'Dxy') | strcmp(name,'Dyx')
        m = 2* floor( n/6) + 1;
        centers = ceil(( 1 :2: 3) * n/4);
        
        Lefts = centers - floor(m/2)-1;
        Rights = centers + floor(m/2);
        Ups = centers - floor(m/2)-1;
        Downs = centers + floor(m/2);
        
        Pos_positives = [ centers , Lefts]
    end
    
end
% %% show
% surf(0:n,0:n,Dxx);
% axis xy; axis tight; view(0, 90);
% Mask  = zeros(n);
% indices = reshape( Pos_borders,1 ,2, size(Pos_borders, 1) );
% Mask(indices) = 1;