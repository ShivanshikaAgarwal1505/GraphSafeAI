import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../models/route_preference.dart';
import '../models/route_response.dart';
import '../providers/navigation_provider.dart';

class RouteSelectorChips extends StatelessWidget {
  const RouteSelectorChips({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    final provider =
        context.watch<NavigationProvider>();

    if (provider.safeRoute == null ||
        provider.balancedRoute == null ||
        provider.fastestRoute == null) {
      return const SizedBox.shrink();
    }

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        _chip(
          context,
          provider,
          'SAFE',
          Colors.green,
          provider.safeRoute!,
          RoutePreference.safe,
        ),

        const SizedBox(height: 8),

        _chip(
          context,
          provider,
          'BALANCED',
          Colors.orange,
          provider.balancedRoute!,
          RoutePreference.balanced,
        ),

        const SizedBox(height: 8),

        _chip(
          context,
          provider,
          'FASTEST',
          Colors.blue,
          provider.fastestRoute!,
          RoutePreference.fastest,
        ),
      ],
    );
  }

  Widget _chip(
    BuildContext context,
    NavigationProvider provider,
    String title,
    Color color,
    RouteResponse route,
    RoutePreference preference,
  ) {
    final selected =
        provider.selectedRoute ==
            preference;

    final safetyScore =
        ((1 -
                    route.riskMetrics
                        .averageRisk) *
                100)
            .round();

    return GestureDetector(
      onTap: () {
        provider.selectRoute(
          preference,
        );
      },
      child: AnimatedContainer(
        duration:
            const Duration(
          milliseconds: 250,
        ),
        width: 64,
        padding:
            const EdgeInsets.symmetric(
              horizontal: 8,
              vertical: 6,
        ),
        decoration: BoxDecoration(
          color: selected
              ? color
              : color.withValues(
                  alpha: 0.5,
                ),
          borderRadius:
              BorderRadius.circular(
            12,
          ),
          boxShadow: selected
              ? [
                  BoxShadow(
                    color: color
                        .withValues(
                      alpha: 0.4,
                    ),
                    blurRadius: 10,
                  ),
                ]
              : [],
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              '$safetyScore',
              style: const TextStyle(
                color: Colors.white,
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),
            Text(
              '${route.metrics.distanceKm.toStringAsFixed(1)}',
              style: const TextStyle(
                color: Colors.white,
                fontSize: 11,
              ),
            ),
          ],
        ),
      ),
    );
  }
}