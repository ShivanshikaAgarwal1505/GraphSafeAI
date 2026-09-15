class RouteMetrics {
  final double distanceKm;
  final int hopCount;

  const RouteMetrics({
    required this.distanceKm,
    required this.hopCount,
  });

  factory RouteMetrics.fromJson(
    Map<String, dynamic> json,
  ) {
    return RouteMetrics(
      distanceKm:
          (json['distance_km'] as num)
              .toDouble(),
      hopCount:
          json['hop_count'] ?? 0,
    );
  }
}