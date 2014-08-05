% Process the data from the telomere experiments.
%
% $AUTHOR: Kyle M. Douglass $ $DATE: 2014/08/05 $ $REVISION: 0.2 $
%

function [distr] = process_data(fileName)
%% Read the text file into memory.
data = tdfread(fileName);

%% Filter out unnecessary columns and condition data for input to DBSCAN.
dataF = [data.Xc data.Yc data.Zc];
clear data

%% Cluster localizations using DBSCAN.
% k - number of objects in a neighborhood of an object 
% (minimal number of objects considered as a cluster)
% Eps - neighborhood radius, if not known avoid this parameter or put []
k = 8;
Eps = 65;
[class, ~] = dbscan(dataF, k, Eps);

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

%% Assign computed values to data structure for return.
distr.M1 = M1;
distr.M2 = M2;
distr.M2Mag = M2Mag;
distr.numLoc = numLoc;
distr.volume = volume;
distr.fileName = fileName;
distr.shortName = 0;

end