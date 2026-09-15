class RouteCoordinate {
  final double latitude;
  final double longitude;

  const RouteCoordinate({
    required this.latitude,
    required this.longitude,
  });

  factory RouteCoordinate.fromJson(
    Map<String, dynamic> json,
  ) {
    return RouteCoordinate(
      latitude:
          (json['latitude'] as num)
              .toDouble(),
      longitude:
          (json['longitude'] as num)
              .toDouble(),
    );
  }
}