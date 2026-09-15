import 'route_coordinate.dart';
import 'route_metrics.dart';
import 'risk_metrics.dart';

class RouteResponse {

  final String profile;

  final double baselineDistanceKm;

  final double maxAllowedDistanceKm;

  final int sourceNode;

  final int destinationNode;

  final int routeLength;

  final List<int> route;

  final List<RouteCoordinate>
      routeCoordinates;

  final RouteMetrics metrics;

  final RiskMetrics riskMetrics;

  const RouteResponse({
    required this.profile,
    required this.baselineDistanceKm,
    required this.maxAllowedDistanceKm,
    required this.sourceNode,
    required this.destinationNode,
    required this.routeLength,
    required this.route,
    required this.routeCoordinates,
    required this.metrics,
    required this.riskMetrics,
  });

  factory RouteResponse.fromJson(
      Map<String, dynamic> json) {

    return RouteResponse(

      profile:
          json['profile'] ?? '',

      baselineDistanceKm:
          (json[
                  'baseline_distance_km']
              as num)
              .toDouble(),

      maxAllowedDistanceKm:
          (json[
                  'max_allowed_distance_km']
              as num)
              .toDouble(),

      sourceNode:
          json['source_node'] ?? 0,

      destinationNode:
          json['destination_node'] ?? 0,

      routeLength:
          json['route_length'] ?? 0,

      route:
          (json['route'] as List?)
                  ?.map(
                    (e) => e as int,
                  )
                  .toList() ??
              [],

      routeCoordinates:
          (json['route_coordinates']
                  as List)
              .map(
                (e) =>
                    RouteCoordinate
                        .fromJson(e),
              )
              .toList(),

      metrics:
          RouteMetrics.fromJson(
        json['metrics'],
      ),

      riskMetrics:
          RiskMetrics.fromJson(
        json['risk_metrics'],
      ),
    );
  }
}