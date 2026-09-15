class RiskMetrics {
  final double averageRisk;
  final double maxRisk;
  final int riskNodeCount;

  const RiskMetrics({
    required this.averageRisk,
    required this.maxRisk,
    required this.riskNodeCount,
  });

  factory RiskMetrics.fromJson(
    Map<String, dynamic> json,
  ) {
    return RiskMetrics(
      averageRisk:
          (json['average_risk'] as num)
              .toDouble(),

      maxRisk:
          (json['max_risk'] as num)
              .toDouble(),

      riskNodeCount:
          json['risk_node_count'] ?? 0,
    );
  }
}