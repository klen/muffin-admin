import { UseMutationOptions, useMutation } from "@tanstack/react-query"
import {
  useDataProvider,
  useNotify,
  useRefresh,
  useResourceContext,
  useUnselectAll,
} from "react-admin"
import { MuffinDataprovider, TActionProps } from "../dataprovider"

export function useAction(
  action: string,
  options?: UseMutationOptions<{ data: any }, any, TActionProps>
) {
  const notify = useNotify()
  const refresh = useRefresh()
  const resource = useResourceContext()
  const unselectAll = useUnselectAll(resource)
  const dataProvider = useDataProvider() as ReturnType<typeof MuffinDataprovider>

  return useMutation({
    mutationFn: (params: TActionProps) => dataProvider.runAction(resource, action, params),
    onSuccess: ({ data }) => {
      if (data && data.message) notify(data.message, { type: "success" })
      if (data && data.redirectTo) window.location = data.redirectTo
      else {
        unselectAll()
        refresh()
      }
    },
    onError: (err) => {
      notify(typeof err === "string" ? err : err.message, { type: "error" })
    },
    ...options,
  })
}
