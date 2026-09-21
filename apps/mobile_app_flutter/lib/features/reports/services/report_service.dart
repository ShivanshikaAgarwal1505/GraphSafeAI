import '../../../core/network/api_client.dart';

import '../models/report_request.dart';
import '../models/community_report.dart';

class ReportService {
  Future<dynamic> submitReport(
      ReportRequest request) {
    return ApiClient.dio.post(
      "/api/v1/reports/",
      data: request.toJson(),
    );
  }

  Future<List<CommunityReport>>
      getReports() async {
    final response =
        await ApiClient.dio.get(
      "/api/v1/reports",
    );

    return (response.data as List)
        .map(
          (item) =>
              CommunityReport.fromJson(
            item,
          ),
        )
        .toList();
  }

  Future<List<CommunityReport>>
      getMyReports() async {
    final response =
        await ApiClient.dio.get(
      "/api/v1/reports/my",
    );

    return (response.data as List)
        .map(
          (item) =>
              CommunityReport.fromJson(
            item,
          ),
        )
        .toList();
  }

  Future<void> closeReport(
  int reportId,
  ) async {
    await ApiClient.dio.patch(
      '/api/v1/reports/$reportId/close',
    );
  }

}