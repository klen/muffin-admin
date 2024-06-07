import { useDataProvider, useResourceContext } from "react-admin"
import { useMutation } from "react-query"
import { TActionProps } from "../dataprovider"

export function useAction(action) {
  const dataProvider = useDataProvider()
  const resource = useResourceContext()
  return useMutation<{ data: any }, { message: string } | string, any>((params: TActionProps) =>
    dataProvider.runAction(resource, action, params)
  )
}
