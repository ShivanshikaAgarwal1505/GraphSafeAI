import 'package:flutter/material.dart';

import '../models/community_report.dart';
import '../services/report_service.dart';

class ReportsProvider
    extends ChangeNotifier {
  final ReportService _service =
      ReportService();

  bool loading = false; 

  List<CommunityReport> reports = [];

  List<CommunityReport>
    allReports = [];

  String selectedFilter =
      'ALL';

  Future<void> loadReports()
      async {
    try {
      loading = true;

      notifyListeners();

      allReports =
        await _service.getMyReports();

    selectedFilter = 'ALL';

    applyFilter(
      selectedFilter,
    );
    
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

  void applyFilter(
    String filter,
  ) {
    selectedFilter = filter;

    if (filter == 'ALL') {
      reports =
          List.from(
        allReports,
      );
    } else {
      reports =
          allReports
              .where(
                (report) =>
                    report.status
                        .toUpperCase() ==
                    filter,
              )
              .toList();
    }

    notifyListeners();
  }
}