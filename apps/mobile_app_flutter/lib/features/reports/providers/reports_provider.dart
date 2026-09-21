import 'package:flutter/material.dart';

import '../models/community_report.dart';
import '../services/report_service.dart';

class ReportsProvider
    extends ChangeNotifier {
  final ReportService _service =
      ReportService();

  bool loading = false;

  List<CommunityReport> reports = [];

  Future<void> loadReports()
      async {
    try {
      loading = true;

      notifyListeners();

      reports =
          await _service.getMyReports();
    } finally {
      loading = false;

      notifyListeners();
    }
  }

  Future<void> closeReport(
    int reportId,
  ) async {
    await _service.closeReport(
      reportId,
    );

    await loadReports();
  }
}