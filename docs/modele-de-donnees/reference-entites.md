# Référence des entités

Champs indicatifs par module. Les identifiants (`id`) et horodatages (`created_at`,
`updated_at`) sont implicites. Légende de statut : ✅ Phase 1 · 🔜 Phase 2/3.

## `identity` — Identité

**User**
: `username` · `email` · `password_hash` · `first_name` · `last_name` · `lang` ·
  `timezone` · `is_active`

**AuthIdentity** 🔜
: `user_id` → User · `provider` (local · oauth · ldap) · `external_id`
: *50+ méthodes possibles ; démarrage en local.*

## `rbac` — Rôles & droits

**Role**
: `shortname` (admin · coursecreator · editingteacher · teacher · student · guest) · `name`

**Capability**
: `name` (ex. `course.manage`, `activity.grade`, `enrol.manage`)

**RoleCapability**
: `role_id` → Role · `capability_id` → Capability · `permission` (allow · prevent)

**RoleAssignment**
: `user_id` → User · `role_id` → Role · `scope_type` (system · category · course) · `scope_id`
: *un utilisateur peut avoir des rôles différents selon la portée.*

## `catalog` — Structure des cours

**Category**
: `parent_id` → Category *(arbre)* · `name` · `path` · `sort_order` · `visible`

**Course**
: `category_id` → Category · `shortname` · `fullname` · `summary` ·
  `format` (weekly · topics) · `start_date` · `end_date` · `visible`

**Section**
: `course_id` → Course · `position` · `name` · `summary` · `visible`

## `activities` — Activités & ressources

**CourseModule** *(enveloppe générique)*
: `course_id` → Course · `section_id` → Section · `kind` · `instance_id` · `position` ·
  `visible` · `completion` · `availability` (conditions d'accès, JSON)

**Assignment** ✅
: `name` · `intro` · `due_at` · `grade_max` · `submission_types`

**Resource** ✅
: `name` · `asset_id` → Asset · `kind` (file · page · url)

**Quiz** · **Forum** 🔜
: + **Question**, **QuestionCategory**, **Attempt** (banque de questions)

## `enrolment` — Inscriptions & groupes

**Enrolment**
: `course_id` → Course · `user_id` → User · `role_id` → Role ·
  `method` (manual · self · cohort) · `status` (active · suspended) · `start_at` · `end_at`

**EnrolmentMethod**
: `course_id` → Course · `type` · `enabled` · `enrol_key` · `default_role_id` · `max`

**Group** / **GroupMember**
: Group : `course_id` · `name` — GroupMember : `group_id` · `user_id`

**Cohort** 🔜
: `scope` · `name` *(inscription en masse à l'échelle de l'établissement)*

## `grades` — Notes & évaluation

**GradeItem**
: `course_id` → Course · `category_id` → GradeCategory · `name` ·
  `source_module_id` → CourseModule *(optionnel)* · `grade_min` · `grade_max` · `weight`

**Grade**
: `grade_item_id` → GradeItem · `user_id` → User · `raw` · `final` · `feedback` ·
  `graded_by` → User · `graded_at`

**GradeCategory** · **Scale** 🔜
: agrégation (mean · sum · weighted) · barèmes non numériques

## `completion` — Achèvement & badges

**ActivityCompletion**
: `course_module_id` → CourseModule · `user_id` → User ·
  `state` (incomplete · complete · passed · failed) · `completed_at`

**CourseCompletion**
: `course_id` → Course · `user_id` → User · `completed_at`

**Badge** / **BadgeAward** 🔜
: Badge : `name` · `criteria` · `image` — BadgeAward : `badge_id` · `user_id` · `awarded_at`

## `files` — Fichiers

**Asset**
: `owner_id` → User · `filename` · `mime` · `size` · `storage_key` ·
  `context` (module · course …)
: *stockage local ou objet (S3) ; référencé par les ressources et les devoirs.*
