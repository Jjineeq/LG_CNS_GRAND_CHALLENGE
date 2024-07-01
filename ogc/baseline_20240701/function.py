import random
import time

def select_two_bundles2(all_bundles, all_riders, dist_mat):
    # DIST : 2K * 2K 행렬
    # 주문 1의 픽업 장소와 주문 2의 픽업 장소 사이의 거리 = DIST[1,2] ---> 이거랑
    # 주문 1의 픽업 장소와 주문 2의 배달 장소 사이의 거리 = DIST[1, 102] : 경로 설정에서 고려
    # 주문 1의 배달 장소와 주문 2의 배달 장소 사이의 거리 = DIST[101, 102] ---> 이거만 고려함
    #start_time = time.time()
    bundle1 = random.sample(all_bundles, 1)[0]
    all_bundles = [bundle for bundle in all_bundles if bundle != bundle1]
    total_volume_bundle1 = bundle1.total_volume
    ready_time_bundle1 = bundle1.all_orders[bundle1.dlv_seq[0]].ready_time
    """
    모든 주문의 volumne을 확인하면서 bundle1의 volume을 더했을 때 차 capa를 넘는 주문 삭제 
    """
    car_capacity = None
    for rider in all_riders:
        if rider.type == 'CAR':
            car_capacity = rider.capa
            break
    bundles_keep_capa = []
    bundles_del_capa = []
    for i, bundle in enumerate(all_bundles):
        combined_volume = total_volume_bundle1 + bundle.total_volume
        if combined_volume <= car_capacity:
            bundles_keep_capa.append(i)
        else:
            bundles_del_capa.append(i)
    capa_all_bundles = [bundle for i, bundle in enumerate(all_bundles) if i not in bundles_del_capa]
    """
    Ready time 비슷한 음식 선택
    """
    bundles_keep_ready_time = []
    bundles_del_ready_time = []
    for i, bundle in enumerate(capa_all_bundles):
        ready_time_bundle = bundle.all_orders[bundle.dlv_seq[0]].ready_time
        if abs(ready_time_bundle - ready_time_bundle1) <= 3500:
            bundles_keep_ready_time.append(i)
        else:
            bundles_del_ready_time.append(i)
    dis_all_bundles = [bundle for i, bundle in enumerate(all_bundles) if i not in bundles_del_ready_time]
    """
    dis_all_bundles 중에서 픽업 장소와 픽업 장소 간의 거리 + 배달 장소와 배달 장소 간의 거리의 합이 작은 주문 선택
    """
    bundle2 = None
    min_distance = float('inf')
    for i, bundle in enumerate(dis_all_bundles):
        pickup_distance = dist_mat[bundle1.dlv_seq[0], bundle.dlv_seq[0]]
        delivery_distance = dist_mat[bundle1.dlv_seq[0] + 100, bundle.dlv_seq[0] + 100]
        total_distance = pickup_distance + delivery_distance
        if total_distance < min_distance:
            min_distance = total_distance
            bundle2 = bundle
    #end_time = time.time()
    #print('select_two_bundles 연신시간(sec)', end_time - start_time)
    return bundle1, bundle2