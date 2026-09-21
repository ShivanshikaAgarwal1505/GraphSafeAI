import 'package:flutter/material.dart';

import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

import '../models/route_response.dart';
import '../models/route_preference.dart';

class RouteMapWidget extends StatelessWidget {
  final RouteResponse? safeRoute;
  final RouteResponse? balancedRoute;
  final RouteResponse? fastestRoute;

  final RoutePreference selectedRoute;

  final double centerLat;
  final double centerLon;

  const RouteMapWidget({
    super.key,
    required this.safeRoute,
    required this.balancedRoute,
    required this.fastestRoute,
    required this.selectedRoute,
    required this.centerLat,
    required this.centerLon,
  });

  @override
  Widget build(BuildContext context) {
    final safePoints =
        safeRoute?.routeCoordinates
                .map(
                  (e) => LatLng(
                    e.latitude,
                    e.longitude,
                  ),
                )
                .toList() ??
            [];

    final balancedPoints =
        balancedRoute?.routeCoordinates
                .map(
                  (e) => LatLng(
                    e.latitude,
                    e.longitude,
                  ),
                )
                .toList() ??
            [];

    final fastestPoints =
        fastestRoute?.routeCoordinates
                .map(
                  (e) => LatLng(
                    e.latitude,
                    e.longitude,
                  ),
                )
                .toList() ??
            [];

    return FlutterMap(
      options: MapOptions(
        initialCenter: LatLng(
          centerLat,
          centerLon,
        ),
        initialZoom: 14,
      ),
      children: [
        TileLayer(
          urlTemplate:
              'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
          userAgentPackageName:
              'com.graphsafeai.app',
        ),

        PolylineLayer(
          polylines: [
            if (safePoints.isNotEmpty)
              Polyline(
                points: safePoints,
                strokeWidth:
                    selectedRoute ==
                            RoutePreference.safe
                        ? 8
                        : 4,
                color:
                    const Color.fromARGB(255, 49, 116, 53)
                        .withValues(
                      alpha:
                        selectedRoute ==
                          RoutePreference.safe
                      ? 1
                      : 0.30,
                ),
              ),

            if (balancedPoints.isNotEmpty)
              Polyline(
                points: balancedPoints,
                strokeWidth:
                    selectedRoute ==
                            RoutePreference
                                .balanced
                        ? 8
                        : 4,
                color:
                    const Color.fromARGB(255, 250, 184, 1)
                        .withValues(
                      alpha:
                        selectedRoute ==
                          RoutePreference
                              .balanced
                      ? 1
                      : 0.30,
                ),
              ),

            if (fastestPoints.isNotEmpty)
              Polyline(
                points: fastestPoints,
                strokeWidth:
                    selectedRoute ==
                            RoutePreference
                                .fastest
                        ? 8
                        : 4,
                color:
                    const Color(0xFF1565C0)
                        .withValues(
                      alpha:
                        selectedRoute ==
                          RoutePreference
                              .fastest
                      ? 1
                      : 0.30,
                ),
              ),
          ],
        ),

        MarkerLayer(
          markers: [
            Marker(
              point: LatLng(
                centerLat,
                centerLon,
              ),
              width: 40,
              height: 40,
              child: const Icon(
                Icons.my_location,
                color: Colors.blue,
                size: 32,
              ),
            ),
          ],
        ),
      ],
    );
  }
}