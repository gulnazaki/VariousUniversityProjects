clear; clc;
% simple example of calling anonymous functions for evaluation

% add path of detectors if necessary
addpath(genpath('../detectors'));
addpath(genpath('../descriptors'));

%% CORNER N=1
s = 2;
r = 2.5;
theta = 0.005;
N = 1;
% detector_func = @(I) multiscale_edge_detect(I, s, r, N) ; 

%% CORNER N=4
N = 4;
% detector_func = @(I) multiscale_edge_detect(I, s, r, N)

%% BLOB N=1
% threshold = 0.01;
% N = 1;
% detector_func = @(I) multiscale_blob_detect( I, N, s);

%% BLOB N=4
N = 4;
% detector_func = @(I) multiscale_blob_detect( I, N, s);

%% BOX FILTERS MULTISCALE N = 4
detector_func = @(I) alt_2_multiscale_blob_detect(I,N);

%%
% example of anonymous function for extracting the SURF features
descriptor_func = @(I,points) featuresSURF(I,points);
% descriptor_func = @(I,points) featuresHOG(I,points);

%%
% get the requested errors, one value for each image in the dataset 
[scale_error,theta_error] = evaluation(detector_func,descriptor_func) ; 