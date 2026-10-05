class FavoriteLocation {

  final int id;

  final String label;

  final double latitude;

  final double longitude;

  const FavoriteLocation({
    required this.id,
    required this.label,
    required this.latitude,
    required this.longitude,
  });

  factory FavoriteLocation.fromJson(
    Map<String, dynamic> json,
  ) {
    return FavoriteLocation(
      id: json['id'],

      label: json['label'],

      latitude:
          (json['latitude']
                  as num)
              .toDouble(),

      longitude:
          (json['longitude']
                  as num)
              .toDouble(),
    );
  }
}