import argparse


class Cluster:

    def __init__(self, centroid):
        self.centroid = centroid
        self.group = []

    def distance(self, other_vector):
        d = len(self.centroid)
        sum = float(0)

        for i in range(0, d):
            difference = float(self.centroid[i] - other_vector[i])
            difference_sqrt = float(difference*difference)
            sum += difference_sqrt

        temp = "{result:.2f}"
        return float(temp.format(result=float(sum)))

    def update_cluster(self):
        d = len(self.centroid)
        result_vector = []

        for i in range(0, d):
            sum = float(0)
            for vector in self.group:
                sum += vector[i]
            sum /= len(self.group)
            temp = "{result:.2f}"
            result_vector.append(float(temp.format(result=sum)))

        self.centroid = result_vector
        self.group = []

    @classmethod
    def initialize_clusters(cls, src, k):
        clusters = []

        for i in range(0, k):
            clusters.append(Cluster(src[i]))

        return clusters

    @classmethod
    def map_observations_to_clusters(cls, observations, clusters):
        for i in range(0, len(observations)):
            cluster_of_closest_centroid = clusters[0]
            min_distance = clusters[0].distance(observations[i])
            for j in range(1, len(clusters)):
                curr_distance = clusters[j].distance(observations[i])
                if curr_distance < min_distance:
                    cluster_of_closest_centroid = clusters[j]
                    min_distance = curr_distance

            cluster_of_closest_centroid.group.append(observations[i])

    @classmethod
    def print_centroids(cls, centroids):
        k = len(centroids)
        d = len(centroids[0])

        for i in range(0, k - 1):
            for j in range(0, d - 1):
                print(centroids[i][j], end=', ')
            print(centroids[i][d - 1])

        for j in range(0, d - 1):
            print(centroids[k - 1][j], end=', ')
        print(centroids[k - 1][d - 1], end='')

    @classmethod
    def are_not_equal(cls, last_calculated_centroids, new_averaged_centroids):
        for i in range(0, len(last_calculated_centroids)):
            if last_calculated_centroids != new_averaged_centroids[i]:
                return False
        return True


# Main
parser = argparse.ArgumentParser()
parser.add_argument("K", type=int)
parser.add_argument("N", type=int)
parser.add_argument("d", type=int)
parser.add_argument("MAX_ITER", type=int)
args = parser.parse_args()

K = args.K
N = args.N
d = args.d
MAX_ITER = args.MAX_ITER

# Initializing observations from input
observations = []

while True:
    try:
        observations.append(input().split(','))
    except EOFError:
        break

for vector in range(0, N):
    for coordinate in range(0, d):
        observations[vector][coordinate] = float(observations[vector][coordinate])

# initializing K clusters objects
clusters = Cluster.initialize_clusters(observations, K)

# storing the first centroids to check later if changed or not
last_calculated_centroids = [cluster.centroid for cluster in clusters]

# do the block below until centroids didn't change or went MAX_ITER times
for iteration in range(0, MAX_ITER):
    # start to map the observations to each cluster
    Cluster.map_observations_to_clusters(observations, clusters)

    # updating each cluster with average centroid and cleaning group
    for i in range(0, K):
        clusters[i].update_cluster()

    new_averaged_centroids = [cluster.centroid for cluster in clusters]

    if Cluster.are_not_equal(last_calculated_centroids, new_averaged_centroids):
        last_calculated_centroids = new_averaged_centroids
    else:
        Cluster.print_centroids(new_averaged_centroids)
        break

    if iteration == MAX_ITER - 1:
        Cluster.print_centroids(new_averaged_centroids)


