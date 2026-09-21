class CommunityReport {
  final int id;

  final int userId;

  final int regionId;

  final double latitude;

  final double longitude;

  final String category;

  final int severity;

  final String description;

  final String status;

  final double confidenceScore;

  final int verificationCount;

  final String source;

  final DateTime timestamp;

  CommunityReport({
    required this.id,
    required this.userId,
    required this.regionId,
    required this.latitude,
    required this.longitude,
    required this.category,
    required this.severity,
    required this.description,
    required this.status,
    required this.confidenceScore,
    required this.verificationCount,
    required this.source,
    required this.timestamp,
  });

  factory CommunityReport.fromJson(
    Map<String, dynamic> json,
  ) {
    return CommunityReport(
      id: json['id'],
      userId: json['user_id']?? 0,
      regionId: json['region_id'],
      latitude: json['latitude'].toDouble(),
      longitude: json['longitude'].toDouble(),
      category: json['category'],
      severity: json['severity'] ?? 3,
      description: json['description'] ?? '',
      status: json['status']?? "OPEN",
      confidenceScore:
          (json['confidence_score'] ?? 0)
              .toDouble(),
      verificationCount:
          json['verification_count'] ?? 0,
      source: json['source'] ?? '',
      timestamp:
          DateTime.parse(
        json['timestamp'] ?? '',
      )?? DateTime.now(),
    );
  }
}
