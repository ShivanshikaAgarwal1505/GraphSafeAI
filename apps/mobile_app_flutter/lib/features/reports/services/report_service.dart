import '../../../core/network/api_client.dart';
import '../models/report_request.dart';

class ReportService {
  Future<dynamic> submitReport(
      ReportRequest request) {
    return ApiClient.dio.post(
      "/api/v1/reports/",
      data: request.toJson(),
    );
  }
}