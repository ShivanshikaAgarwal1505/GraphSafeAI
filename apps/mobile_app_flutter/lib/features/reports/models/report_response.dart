class ReportResponse {
  final int id;

  final String message;

  const ReportResponse({
    required this.id,
    required this.message,
  });

  factory ReportResponse.fromJson(
    Map<String, dynamic> json,
  ) {
    return ReportResponse(
      id: json["id"] ?? 0,
      message:
          json["message"] ?? "",
    );
  }
}