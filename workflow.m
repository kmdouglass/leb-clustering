% Workflow for analysis of the telomere data
%
% $AUTHOR: Kyle M. Douglass $ $DATE: 2014/07/23 $ $REVISION: 0.1 $
% 
%% Read localization data into memory.
%workDir = 'Z:\LEB\Users\Kyle-Michael-Douglass\Projects\Telomeres\';
workDir = '/mnt/LEBZ/Users/Kyle-Michael-Douglass/Projects/Telomeres/';

%fName = '11_06_2014_FISH_HelaL_8_list.txt';
fName = '11_06_2014_FISH_HelaL_slide2_8_list.txt';
%fName = '11_06_2014_FISH_HelaS_slide3_7_list.txt';
%fName = '11_06_2014_FISH_HelaS_slide3_10_list.txt';

data = tdfread([workDir fName]);

%% Filter out unnecessary columns and condition data for input to DBSCAN.
dataF = [data.Xc data.Yc data.Zc];

%% Cluster localizations using DBSCAN.
% k - number of objects in a neighborhood of an object 
% (minimal number of objects considered as a cluster)
% Eps - neighborhood radius, if not known avoid this parameter or put []
k = 8;
Eps = 65;
tic
[class, type] = dbscan(dataF, k, Eps);
toc

%% Check histogram of localization types
%hist(type)

%% Filter noise localizations out of data.
% DBSCAN labels noise, border, and core points as -1, 0, and 1, respect.
% datacl = datac(type >= 0,:);
% classcl = class(type >= 0);

%% Separate clusters.
numClusters = max(class);
clusters = cell(numClusters + 1,1);

for ctr = 1:numClusters
    clusters{ctr} = dataF(class == ctr, :);
end
% Save noise points in the last element of the 'clusters' array.
clusters{end} = dataF(class == -1, :);

%% Count the number of localizations within each cluster and noise points.
numLoc = zeros(numClusters + 1,1);

for ctr = 1:numClusters
    [numLoc(ctr), ~] = size(clusters{ctr});
end
[numLoc(end), ~] = size(clusters{end});

%% Filter the clusters by number of localizations.
% Remove clusters with fewer than minLoc localizations
% Minimum number of labels/telomere assuming 100% labeling efficiency: 220
% Maximum number of labels/telomere assuming 100% labeling efficiency: 1670
minLoc = 50;

clustersF = clusters(cellfun(@length, clusters) > minLoc);
numClustersF = length(clustersF) - 1;

%% Plot filtered clusters in 3D.
% See, for example, <http://stackoverflow.com/questions/5492806/plotting-a-surface-from-a-set-of-interior-3d-scatter-points-in-matlab>
hold on
for ctr = 1:numClustersF
    DT = DelaunayTri(clustersF{ctr});
    hullFacets = convexHull(DT);
    
    trisurf(hullFacets,DT.X(:,1),DT.X(:,2),DT.X(:,3),'FaceColor',rand(1,3))
    axis equal
end
hold off
grid on

%% Plot 3D scatter plot of all data points.
scatter3(dataF(:,1),dataF(:,2),dataF(:,3), '.k')
axis equal
grid on

%% Plot 3D scatter plot of cluster points and noise points.
hold on
for ctr = 1:numClustersF
    scatter3(clustersF{ctr}(:,1), clustersF{ctr}(:,2), clustersF{ctr}(:,3),'.')
end
scatter3(clustersF{end}(:,1), clustersF{end}(:,2), clustersF{end}(:,3),'k+','SizeData',10)
hold off
axis equal
grid on

