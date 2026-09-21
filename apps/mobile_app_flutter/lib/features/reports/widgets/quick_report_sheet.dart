import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../location/providers/location_provider.dart';

import '../models/report_request.dart';
import '../services/report_service.dart';

class QuickReportSheet extends StatefulWidget {
  const QuickReportSheet({
    super.key,
  });

  @override
  State<QuickReportSheet> createState() =>
      _QuickReportSheetState();
}

class _QuickReportSheetState
    extends State<QuickReportSheet> {
  bool loading = false;

  Future<void> submitReport(
    String category,
  ) async {
    final locationProvider =
        context.read<LocationProvider>();

    final position =
        locationProvider.position;

    if (position == null) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Location unavailable',
          ),
        ),
      );

      return;
    }

    try {
      setState(() {
        loading = true;
      });

      final service = ReportService();

      await service.submitReport(
        ReportRequest(
          latitude:
              position.latitude,
          longitude:
              position.longitude,
          category: category,
          severity: 3,
          description: category,
          source: "USER",
          timestamp:
              DateTime.now(),
        ),
      );

      if (!mounted) return;

      Navigator.pop(context);

      ScaffoldMessenger.of(context)
          .showSnackBar(
        SnackBar(
          content: Text(
            '$category report submitted',
          ),
        ),
      );
    } catch (e) {
      if (!mounted) return;

      ScaffoldMessenger.of(context)
          .showSnackBar(
        SnackBar(
          content: Text(
            'Failed to submit report',
          ),
        ),
      );
    } finally {
      if (mounted) {
        setState(() {
          loading = false;
        });
      }
    }
  }

  Widget buildButton({
    required IconData icon,
    required String title,
    required String category,
    required Color color,
  }) {
    return SizedBox(
      width: double.infinity,
      child: FilledButton.icon(
        style: FilledButton.styleFrom(
          backgroundColor: color,
          padding:
              const EdgeInsets.symmetric(
            vertical: 14,
          ),
        ),
        onPressed: loading
            ? null
            : () => submitReport(
                  category,
                ),
        icon: Icon(icon),
        label: Text(title),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Padding(
        padding:
            EdgeInsets.only(
          left: 20,
          right: 20,
          top: 20,
          bottom:
              MediaQuery.of(context)
                      .viewInsets
                      .bottom +
                  20,
        ),
        child: Column(
          mainAxisSize:
              MainAxisSize.min,
          children: [
            Container(
              width: 50,
              height: 5,
              decoration:
                  BoxDecoration(
                color: Colors.grey[400],
                borderRadius:
                    BorderRadius
                        .circular(10),
              ),
            ),

            const SizedBox(
              height: 20,
            ),

            const Text(
              'Quick Report',
              style: TextStyle(
                fontSize: 22,
                fontWeight:
                    FontWeight.bold,
              ),
            ),

            const SizedBox(
              height: 8,
            ),

            Text(
              'Report incidents at your current location',
              textAlign:
                  TextAlign.center,
              style: TextStyle(
                color: Colors.grey[600],
              ),
            ),

            const SizedBox(
              height: 24,
            ),

            buildButton(
              icon: Icons.warning,
              title:
                  'Report Harassment',
              category:
                  'Harassment',
              color:
                  Colors.orange,
            ),

            const SizedBox(
              height: 12,
            ),

            buildButton(
              icon:
                  Icons.security,
              title:
                  'Report Theft',
              category: 'Theft',
              color: Colors.red,
            ),

            const SizedBox(
              height: 12,
            ),

            buildButton(
              icon: Icons.report,
              title:
                  'Poor Lighting',
              category:
                  'Poor Lighting',
              color:
                  Colors.indigo,
            ),

            const SizedBox(
              height: 12,
            ),

            buildButton(
              icon:
                  Icons.warning_amber,
              title:
                  'Other Incident',
              category: 'Other',
              color:
                  Colors.blueGrey,
            ),

            if (loading) ...[
              const SizedBox(
                height: 24,
              ),
              const CircularProgressIndicator(),
            ],
          ],
        ),
      ),
    );
  }
}