# Accessibility (A11y) Baseline & Audit Protocol

## A11y Baseline (Always on new configs)

Every new configuration must include this foundational structure:

```typescript
accessibility: {
  enabled: true,
  description: '', // caller fills: what chart shows + key insight
  point: { valueDescriptionFormat: '{index}. {point.category}: {point.y}.' },
},
credits: { enabled: false },
```

## WCAG 2.2 Audit Protocol

When evaluating an existing config for accessibility, verify the following:
1. `accessibility.enabled` is explicitly `true`
2. `accessibility.description` provides meaningful context about the data (not just "a chart")
3. Screen reader formatters (e.g. `point.valueDescriptionFormat`) provide clear numerical reading
4. Legend is keyboard-navigable and `accessibility.keyboardNavigation.enabled` is not explicitly disabled
5. Colors meet 3:1 minimum contrast for large text / data points, 4.5:1 for standard text (verify with `colors` array)
