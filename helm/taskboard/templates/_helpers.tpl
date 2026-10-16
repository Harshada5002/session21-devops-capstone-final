{{/*
Common labels applied to all resources.
*/}}
{{- define "taskboard.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}

{{/*
Selector labels for a given component (backend | frontend | postgresql).
*/}}
{{- define "taskboard.selectorLabels" -}}
app.kubernetes.io/name: taskboard
app.kubernetes.io/component: {{ . }}
{{- end }}
