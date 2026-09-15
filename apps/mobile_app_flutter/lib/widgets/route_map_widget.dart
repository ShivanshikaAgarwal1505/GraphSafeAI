import 'package:flutter/material.dart';

import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

import '../models/route_coordinate.dart';

class RouteMapWidget extends StatelessWidget {

  final List<RouteCoordinate>
      coordinates;

  const RouteMapWidget({
    super.key,
    required this.coordinates,
  });

  @override
  Widget build(
      BuildContext context) {

    if (coordinates.isEmpty) {
      return const SizedBox();
    }

    final points =
        coordinates
            .map(
              (e) => LatLng(
                e.latitude,
                e.longitude,
              ),
            )
            .toList();

    final source =
        points.first;

    final destination =
        points.last;

    return Card(

      child: SizedBox(

        height: 500,

        child: FlutterMap(

          options: MapOptions(

            initialCenter:
                source,

            initialZoom: 15,
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

                Polyline(

                  points: points,

                  strokeWidth: 4,

                  color: Colors.blue,
                ),
              ],
            ),

            MarkerLayer(

              markers: [

                Marker(

                  point: source,

                  width: 40,

                  height: 40,

                  child: const Icon(
                    Icons.location_on,
                    color: Colors.green,
                    size: 36,
                  ),
                ),

                Marker(

                  point:
                      destination,

                  width: 40,

                  height: 40,

                  child: const Icon(
                    Icons.flag,
                    color: Colors.red,
                    size: 36,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}