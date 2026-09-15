import 'package:flutter/material.dart';

class QuickReportSheet
    extends StatelessWidget {

  const QuickReportSheet({
    super.key,
  });

  @override
  Widget build(
      BuildContext context) {

    return Padding(

      padding:
          const EdgeInsets.all(20),

      child: Column(

        mainAxisSize:
            MainAxisSize.min,

        children: [

          const Text(
            'Quick Report',
            style: TextStyle(
              fontSize: 22,
              fontWeight:
                  FontWeight.bold,
            ),
          ),

          const SizedBox(
            height: 20,
          ),

          FilledButton.icon(

            onPressed: () {},

            icon:
                const Icon(
              Icons.warning,
            ),

            label: const Text(
              'Report Harassment',
            ),
          ),

          FilledButton.icon(

            onPressed: () {},

            icon:
                const Icon(
              Icons.security,
            ),

            label: const Text(
              'Report Theft',
            ),
          ),

          FilledButton.icon(

            onPressed: () {},

            icon:
                const Icon(
              Icons.report,
            ),

            label: const Text(
              'Other Incident',
            ),
          ),
        ],
      ),
    );
  }
}