import 'package:flutter/material.dart';

import '../models/report_request.dart';
import '../models/report_response.dart';
import '../services/report_service.dart';

class ReportsProvider
    extends ChangeNotifier {

  final ReportService _service =
      ReportService();

  bool loading = false;

  ReportResponse? response;

  Future<void> submitReport(
      ReportRequest request) async {

    loading = true;

    notifyListeners();

    try {

      final result =
          await _service
              .submitReport(
        request,
      );

      response =
          ReportResponse.fromJson(
        result.data,
      );

    } finally {

      loading = false;

      notifyListeners();
    }
  }
}