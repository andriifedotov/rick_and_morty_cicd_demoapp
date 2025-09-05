{{- define "rickmorty-api.name" -}}
rickmorty-api
{{- end -}}

{{- define "rickmorty-api.fullname" -}}
{{ .Release.Name }}-{{ include "rickmorty-api.name" . }}
{{- end -}}
