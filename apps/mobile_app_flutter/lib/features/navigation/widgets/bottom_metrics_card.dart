import 'package:flutter/material.dart';

import '../models/route_response.dart';

class BottomMetricsCard
    extends StatelessWidget {

  final RouteResponse route;

  const BottomMetricsCard({
    super.key,
    required this.route,
  });

  @override
  Widget build(
      BuildContext context) {

    return Card(

      elevation: 8,

      child: Padding(

        padding:
            const EdgeInsets.all(
                16),

        child: Row(

          mainAxisAlignment:
              MainAxisAlignment
                  .spaceAround,

          children: [

            Column(
              mainAxisSize:
                  MainAxisSize.min,

              children: [

                const Text(
                  'Distance',
                ),

                Text(
                  '${route.metrics.distanceKm} km',
                ),
              ],
            ),

            Column(
              mainAxisSize:
                  MainAxisSize.min,

              children: [

                const Text(
                  'Risk',
                ),

                Text(
                  route
                      .riskMetrics
                      .averageRisk
                      .toStringAsFixed(
                          3),
                ),
              ],
            ),

            Column(
              mainAxisSize:
                  MainAxisSize.min,

              children: [

                const Text(
                  'Nodes',
                ),

                Text(
                  route.routeLength
                      .toString(),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}