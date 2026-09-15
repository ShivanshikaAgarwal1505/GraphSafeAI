import 'package:flutter/material.dart';

import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

import '../models/route_coordinate.dart';

class RouteMapWidget
    extends StatelessWidget {

  final List<RouteCoordinate>
      coordinates;

  final double centerLat;

  final double centerLon;

  const RouteMapWidget({
    super.key,
    required this.coordinates,
    required this.centerLat,
    required this.centerLon,
  });

  @override
  Widget build(
      BuildContext context) {

    final points =
        coordinates
            .map(
              (e) => LatLng(
                e.latitude,
                e.longitude,
              ),
            )
            .toList();

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

        if (points.isNotEmpty)

          PolylineLayer(
            polylines: [
              Polyline(
                points: points,
                strokeWidth: 7,
                color: const Color(0xFF0066FF,),
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