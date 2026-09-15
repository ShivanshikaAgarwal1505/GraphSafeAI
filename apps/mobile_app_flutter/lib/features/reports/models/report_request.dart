class ReportRequest {
  final double latitude;
  final double longitude;

  final String category;

  final int severity;

  final String description;

  final String source;

  final DateTime timestamp;

  const ReportRequest({
    required this.latitude,
    required this.longitude,
    required this.category,
    required this.severity,
    required this.description,
    required this.source,
    required this.timestamp,
  });

  Map<String, dynamic> toJson() {
    return {
      "latitude": latitude,
      "longitude": longitude,
      "category": category,
      "severity": severity,
      "description": description,
      "source": source,
      "timestamp":
          timestamp.toIso8601String(),
    };
  }
}