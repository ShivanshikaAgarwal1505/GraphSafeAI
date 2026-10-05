import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

import '../models/route_response.dart';
import '../models/route_preference.dart';

class RouteMapWidget extends StatefulWidget {
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
  State<RouteMapWidget> createState() =>
      _RouteMapWidgetState();
}

class _RouteMapWidgetState
    extends State<RouteMapWidget> {
  final MapController mapController =
      MapController();

  void _fitRoute(
    List<LatLng> points,
  ) {
    if (points.isEmpty) {
      return;
    }

    double minLat =
        points.first.latitude;

    double maxLat =
        points.first.latitude;

    double minLon =
        points.first.longitude;

    double maxLon =
        points.first.longitude;

    for (final point in points) {
      if (point.latitude < minLat) {
        minLat = point.latitude;
      }

      if (point.latitude > maxLat) {
        maxLat = point.latitude;
      }

      if (point.longitude < minLon) {
        minLon = point.longitude;
      }

      if (point.longitude > maxLon) {
        maxLon = point.longitude;
      }
    }

    mapController.fitCamera(
      CameraFit.bounds(
        bounds: LatLngBounds(
          LatLng(minLat, minLon),
          LatLng(maxLat, maxLon),
        ),
        padding:
            const EdgeInsets.all(60),
      ),
    );
  }

  @override
  void didUpdateWidget(
    covariant RouteMapWidget oldWidget,
  ) {
    super.didUpdateWidget(oldWidget);

    RouteResponse? route;

    switch (
        widget.selectedRoute) {
      case RoutePreference.safe:
        route = widget.safeRoute;
        break;

      case RoutePreference.balanced:
        route =
            widget.balancedRoute;
        break;

      case RoutePreference.fastest:
        route =
            widget.fastestRoute;
        break;
    }

    if (route == null ||
        route.routeCoordinates
            .isEmpty) {
      return;
    }

    final points =
        route.routeCoordinates
            .map(
              (e) => LatLng(
                e.latitude,
                e.longitude,
              ),
            )
            .toList();

    WidgetsBinding.instance
        .addPostFrameCallback(
      (_) {
        _fitRoute(points);
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final safePoints =
        widget.safeRoute
                ?.routeCoordinates
                .map(
                  (e) => LatLng(
                    e.latitude,
                    e.longitude,
                  ),
                )
                .toList() ??
            [];

    final balancedPoints =
        widget.balancedRoute
                ?.routeCoordinates
                .map(
                  (e) => LatLng(
                    e.latitude,
                    e.longitude,
                  ),
                )
                .toList() ??
            [];

    final fastestPoints =
        widget.fastestRoute
                ?.routeCoordinates
                .map(
                  (e) => LatLng(
                    e.latitude,
                    e.longitude,
                  ),
                )
                .toList() ??
            [];

    return FlutterMap(
      mapController:
          mapController,
      options: MapOptions(
        initialCenter: LatLng(
          widget.centerLat,
          widget.centerLon,
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
                    widget.selectedRoute ==
                            RoutePreference.safe
                        ? 8
                        : 4,
                color:
                    const Color.fromARGB(
                      255,
                      49,
                      116,
                      53,
                    ).withValues(
                  alpha:
                      widget.selectedRoute ==
                              RoutePreference.safe
                          ? 1
                          : 0.30,
                ),
              ),

            if (balancedPoints
                .isNotEmpty)
              Polyline(
                points:
                    balancedPoints,
                strokeWidth:
                    widget.selectedRoute ==
                            RoutePreference
                                .balanced
                        ? 8
                        : 4,
                color:
                    const Color.fromARGB(
                      255,
                      250,
                      184,
                      1,
                    ).withValues(
                  alpha:
                      widget.selectedRoute ==
                              RoutePreference
                                  .balanced
                          ? 1
                          : 0.30,
                ),
              ),

            if (fastestPoints
                .isNotEmpty)
              Polyline(
                points:
                    fastestPoints,
                strokeWidth:
                    widget.selectedRoute ==
                            RoutePreference
                                .fastest
                        ? 8
                        : 4,
                color:
                    const Color(
                      0xFF1565C0,
                    ).withValues(
                  alpha:
                      widget.selectedRoute ==
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
                widget.centerLat,
                widget.centerLon,
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