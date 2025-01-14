% Script for data mining in the telomere data.
%
% $AUTHOR: Kyle M. Douglass $ $DATE: 2014/08/13 $ $REVISION: 0.4 $
% 
%% Read localization data into memory.
%workDir = 'Z:\LEB\Users\Kyle-Michael-Douglass\Projects\Telomeres\';
%workDir = '~/Data/30_07_2014_HeLaS_L_SmchD1_KD_FISH/30_07_2014_HelaL_SmchD1_pSuper_mol_list/';
%workDir = '~/Data/30_07_2014_HeLaS_L_SmchD1_KD_FISH/30_07_2014_HelaL_SmchD1_pLVP041_mol_list/';
%workDir = '~/Data/30_07_2014_HeLaS_L_SmchD1_KD_FISH/30_07_2014_HelaL_SmchD1_pLVP042_mol_list/';
%workDir = '~/Data/30_07_2014_HeLaS_L_SmchD1_KD_FISH/30_07_2014_HelaS_SmchD1_pLVP042_mol_list/';
workDir = '~/Data/30_07_2014_HeLaS_L_SmchD1_KD_FISH/30_07_2014_HelaS_SmchD1_pLVP041_mol_list/';

imgDir = [workDir(1:end-17) 'KD_FISH_pLVP041/'];

%fName = '30_07_2014_HelaL_SmchD1_KD_FISH_pSuper_1_list.txt';
%fName = '30_07_2014_HelaL_SmchD1_KD_FISH_pSuper_5_list.txt';
%fName = '30_07_2014_HelaL_SmchD1_KD_FISH_pLVP041_2_list.txt';
%fName = '30_07_2014_HelaL_SmchD1_KD_FISH_pLVP041_10_list.txt';
%fName = '30_07_2014_HelaL_SmchD1_KD_FISH_pLVP042_8_list.txt';
%fName = '30_07_2014_HelaS_SmchD1_KD_FISH_pLVP042_8_list.txt';
fName = '30_07_2014_HelaS_SmchD1_KD_FISH_pLVP041_14_list.txt';

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

%% Check histogram of localization types.
%hist(type)

%% Filter noise localizations out of data.
% DBSCAN labels noise, border, and core points as -1, 0, and 1, respect.
% datacl = datac(type >= 0,:);
% classcl = class(type >= 0);

%% Separate clusters.
numClusters = max(class);
clusters = cell(numClusters,1);

for ctr = 1:numClusters
    clusters{ctr} = dataF(class == ctr, :);
end

% Save noise points in a separate array.
noise = dataF(class == -1, :);

%% Filter the clusters by number of localizations.
% Remove clusters with fewer than minLoc localizations
% Minimum number of labels/telomere assuming 100% labeling efficiency: 220
% Maximum number of labels/telomere assuming 100% labeling efficiency: 1670
minLoc = 50;

clustersF = clusters(cellfun(@length, clusters) > minLoc);
numClustersF = length(clustersF);

%% Plot 3D scatter plot of all data points.
% scatter3(dataF(:,1),dataF(:,2),dataF(:,3), '.k')
% axis equal
% grid on

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

%% Plot 3D scatter plot of cluster points and noise points.
hold on
for ctr = 1:numClustersF
    scatter3(clustersF{ctr}(:,1), clustersF{ctr}(:,2), clustersF{ctr}(:,3),'.')
end
% This also assumes that noise is the last row.
scatter3(noise(:,1), noise(:,2), noise(:,3),'k+','SizeData',10)
hold off
axis equal
grid on

%% Plot clustered points on top of wide field images.
dateLength = 11;
removeLength = 9;
fType = '.jp2';
fNameImg = [fName(1:dateLength) fType];

% Distance-to-pixel conversion factor
dist2pix = 1/160;

img = imread([imgDir fName(1:dateLength) 'WF' fName(dateLength:end-removeLength) fType]);
imshow(img, [min(img(:)) max(img(:))])
hold on
for ctr = 1:numClustersF
    plot(dist2pix * clustersF{ctr}(:,1), dist2pix * clustersF{ctr}(:,2), 'r+')
end
hold off

%% Find moments of the distribution of localizations within the clusters.
% Rows of M1 are the first moments of the distribution for each coordinate
% of the localizations within a single cluster.
%
% M2 is the diagonal of the covariance matrix computed from the
% (Xc, Yc, Zc) positions of the points within a cluster. Each row is the
% covariance matrix diagonal of a different cluster.
M1 = cell2mat(cellfun(@mean, clustersF, 'UniformOutput', false));
M2 = cell2mat(cellfun(@second_central_moment, clustersF, 'UniformOutput', false));

% Magnitude of the second moment
M2Mag = sqrt(sum(M2,2));

%% Count the number of localizations within each cluster and noise points.
numLoc = zeros(numClustersF,1);

for ctr = 1:numClustersF
    [numLoc(ctr), ~] = size(clustersF{ctr});
end

%% Determine the volume of the complex hull defined by the clusters.
% See: <http://scicomp.stackexchange.com/questions/8089/volume-of-3d-convex-hull-of-small-point-sets-all-on-the-hull>
volume = zeros(numClustersF,1);

for ctr = 1:numClustersF
    DT = DelaunayTri(clustersF{ctr});
    t = DT.Triangulation;
    e1 = clustersF{ctr}(t(:,2),:) - clustersF{ctr}(t(:,1),:);
    e2 = clustersF{ctr}(t(:,3),:) - clustersF{ctr}(t(:,1),:);
    e3 = clustersF{ctr}(t(:,4),:) - clustersF{ctr}(t(:,1),:);
    V = abs(dot(cross(e1,e2,2),e3,2))/6;
    volume(ctr) = sum(V);
end

%% Plot the histogram of second central moments.
hist(M2)
title('Distribution of the variances from clustered groups of localizations about the x, y, and z axes')
xlabel('Variance, nm^2')
ylabel('Number of occurrences')
legend('M_x^2', 'M_y^2', 'M_z^2')
grid on

%% Plot the histogram of magnitude of second moments.
hist(M2Mag)
title('Distribution of the magnitudes of R_g from clustered groups of localizations')
xlabel('R_g, nm')
ylabel('Number of occurrences')
grid on

%% Plot the histogram of the number of localizations.
hist(numLoc)
title('Distribution of the number of localizations per cluster')
xlabel('Number of localizations')
ylabel('Number of occurrences')
grid on

%% Plot the histogram of the volumes of the complex hulls.
hist(volume)
title('Distribution of the volumes of the complex hulls of the clusters')
xlabel('Volume, nm^3')
ylabel('Number of occurrences')
grid on

%% Make a scatter plot of the magnitude of M2 vs. the cube root of volume.
x = volume.^(1/3);
y = M2Mag;

p = polyfit(x, y, 1);
linearFit = polyval(p, x);
resid = y - linearFit;
SSresid = sum(resid.^2);
SStotal = (length(y) -1) * var(y);
Rsq = 1 - SSresid/SStotal;

scatter(volume.^(1/3),M2Mag)
hold on
plot(volume.^(1/3), linearFit, 'k')
hold off
title('Second central moments vs the cube root of volume of clusters')
xlabel('Cube root of volume, nm')
ylabel('(|M^2|)^{1/2}, nm')
legend('Size of clusters', ['Linear regression (R^2 = ' num2str(Rsq, '%.2f') ')'], 'Location', 'SouthEast')
grid on