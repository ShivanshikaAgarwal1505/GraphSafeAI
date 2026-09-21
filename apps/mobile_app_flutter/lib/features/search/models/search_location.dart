class SearchLocation {
  final String name;
  final double latitude;
  final double longitude;
  final bool isCurrentLocation;

  const SearchLocation({
    required this.name,
    required this.latitude,
    required this.longitude,
    this.isCurrentLocation = false,
  });

  factory SearchLocation.current() {
    return const SearchLocation(
      name: 'Current Location',
      latitude: 0,
      longitude: 0,
      isCurrentLocation: true,
    );
  }

  factory SearchLocation.fromJson(
    Map<String, dynamic> json,
  ) {
    return SearchLocation(
      name: json['name'],
      latitude:
          (json['latitude'] as num)
              .toDouble(),
      longitude:
          (json['longitude'] as num)
              .toDouble(),
      isCurrentLocation:
          json['isCurrentLocation'] ??
              false,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'latitude': latitude,
      'longitude': longitude,
      'isCurrentLocation':
          isCurrentLocation,
    };
  }
}