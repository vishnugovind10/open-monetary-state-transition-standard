# RFC-0015: Finality

Status: draft

## Abstract

Defines OMST finality vocabulary and the distinction between technical, economic, legal and operational finality.

## Motivation

Finality is a core settlement constraint and cannot be reduced to one unqualified label.

## Scope

Conceptual vocabulary in v0.3.

## Terminology

Probabilistic, deterministic, economic, legal, operational, qualified, unknown.

## Specification

See `docs/settlement/finality.md`.

## Examples

Qualified finality within 60 seconds for a synthetic DvP.

## Security Considerations

Required finality cannot be silently relaxed.

## Privacy Considerations

No special privacy considerations.

## Compatibility

Clarifies existing fields.

## Open Questions

How should legal-finality evidence be represented without legal advice?
