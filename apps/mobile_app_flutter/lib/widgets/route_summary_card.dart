import 'package:flutter/material.dart';

import '../models/route_response.dart';
import 'risk_badge.dart';

class RouteSummaryCard
    extends StatelessWidget {

  final RouteResponse route;

  const RouteSummaryCard({
    super.key,
    required this.route,
  });

  @override
  Widget build(
      BuildContext context) {

    return Card(

      child: Padding(
        padding:
            const EdgeInsets.all(
                16),

        child: Column(

          crossAxisAlignment:
              CrossAxisAlignment
                  .start,

          children: [

            const Text(
              "Route Summary",
              style: TextStyle(
                fontSize: 20,
                fontWeight:
                    FontWeight.bold,
              ),
            ),

            const SizedBox(
              height: 12,
            ),

            Text(
              "Profile: ${route.profile}",
            ),

            Text(
              "Distance: ${route.metrics.distanceKm} km",
            ),

            Text(
              "Node Count: ${route.routeLength}",
            ),

            Text(
              "Hop Count: ${route.metrics.hopCount}",
            ),

            Text(
              "Source Node: ${route.sourceNode}",
            ),

            Text(
              "Destination Node: ${route.destinationNode}",
            ),

            const SizedBox(
              height: 10,
            ),

            RiskBadge(
              risk: route
                  .riskMetrics
                  .averageRisk,
            ),

            const SizedBox(
              height: 6,
            ),

            RiskBadge(
              risk: route
                  .riskMetrics
                  .maxRisk,
            ),
          ],
        ),
      ),
    );
  }
}