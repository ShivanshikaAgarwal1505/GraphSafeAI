import 'package:flutter/material.dart';

import '../models/route_response.dart';

class ComparisonCard
    extends StatelessWidget {

  final RouteResponse route;

  const ComparisonCard({
    super.key,
    required this.route,
  });

  @override
  Widget build(
      BuildContext context) {

    return Card(

      child: ListTile(

        title:
            Text(route.profile),

        subtitle:
            Text(
          'Distance: ${route.metrics.distanceKm} km',
        ),

        trailing:
            Column(

          mainAxisAlignment:
              MainAxisAlignment.center,

          children: [

            Text(
              route.riskMetrics
                  .averageRisk
                  .toStringAsFixed(
                      3),
            ),

            const Text(
              'Risk',
            ),
          ],
        ),
      ),
    );
  }
}