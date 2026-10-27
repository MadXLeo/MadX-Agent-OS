# MadX security implementation boundaries

The inherited threat model remains in ../../SECURITY.md. The baseline retains loopback-only Hermes,
per-launch tokens, sandboxed/context-isolated renderers, isolated web/preview partitions, protected
credential paths and audited permission tiers. These are code boundaries to preserve and test,
not a claim that this fork has passed an independent security review.

New model/adapter/dataset inputs must have bounded sizes and parsers, canonical-path checks,
digest/provenance records and atomic writes. Reject pickle and executable adapter packages.
Archive import requires traversal, symlink, decompression-bomb and duplicate checks. No renderer
or imported workflow may choose arbitrary subprocess arguments or access API credentials.

Long-running workers require cancellation, timeouts, resource limits and explicit filesystem/
network scopes. AI workers must not run as unrestricted root. Privileged operations go through
small authenticated helpers, explicit approvals and durable audit events. Training and proposed
code cannot alter the approval broker, its security policy or audit retention.

External content, model output, imported workflow descriptions and generated skills are untrusted
data. They cannot supply permissions. Promotion of a skill, adapter or software change is distinct
from generating it and requires appropriate validation and user approval.

No training on all conversations. Approved datasets require sensitivity review, deduplication and
deletion/export controls. Model metrics and adapter comparisons must name the fixed evaluation set
and baseline. No automatic promotion based on an agent's own assertion of success.

Installer testing uses disposable virtual disks only. Host partitions, EFI, Windows boot files and
firmware entries are outside development scope. Publication and registry credentials are not used
without authorization. Preserve upstream licenses and notices in every release artifact.
