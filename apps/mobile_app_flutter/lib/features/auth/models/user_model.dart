class UserModel {
  final int id;

  final String name;

  final String email;

  final int reputationScore;

  final int reportsSubmitted;

  final int reportsVerified;

  UserModel({
    required this.id,
    required this.name,
    required this.email,
    required this.reputationScore,
    required this.reportsSubmitted,
    required this.reportsVerified,
  });

  factory UserModel.fromJson(
    Map<String, dynamic> json,
  ) {
    return UserModel(
      id: json['id'],
      name: json['name'],
      email: json['email'],
      reputationScore:
          json['reputation_score'] ?? 0,
      reportsSubmitted:
          json['reports_submitted'] ?? 0,
      reportsVerified:
          json['reports_verified'] ?? 0,
    );
  }
}