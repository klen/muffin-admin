import { useDataProvider, useResourceContext } from "react-admin"
import { UseMutationOptions, useMutation } from "react-query"
import { MuffinDataprovider, TActionProps } from "../dataprovider"

export function useAction(
  action: string,
  options?: UseMutationOptions<{ data: any }, any, TActionProps>
) {
  const resource = useResourceContext()
  const dataProvider = useDataProvider() as ReturnType<typeof MuffinDataprovider>
  return useMutation(
    (params: TActionProps) => dataProvider.runAction(resource, action, params),
    options
  )
}
