__all__ = ['code_activity_bp']
from quart import Blueprint, request, jsonify
from src.types import ApiResponse
from src.services import update_code_activity
from src.auth import token_required
from src.types import CodeActivityRequest as CAR
from src.configs import RedisKeynameConfig
from src.globals import get_redis

cabp = code_activity_bp = Blueprint('code_activity',
                                    __name__,
                                    static_folder='../../static')


@cabp.post('/activities')
@token_required()
async def update_activities(userid: int, token: str):
  data = await request.get_json()
  try:
    activity = CAR(**data)
  except Exception as e:
    res = ApiResponse(None, 'Invalid request body', 'A0400', repr(e))
    return jsonify(res.to_dict()), 400
  # 使用redis去重
  redis = await get_redis()
  async with redis.client() as conn:
    exist = await redis.sismember(RedisKeynameConfig().CODE_ACTIVITY_REQUEST, # type: ignore
                            str(activity.id))
    if exist:
      res = ApiResponse(None, 'Duplicate request', 'A0401')
      return jsonify(res.to_dict()), 400

  try:

    await update_code_activity(userid, activity)
    # 记录请求到redis
    async with redis.client() as conn:
      await conn.sadd(RedisKeynameConfig().CODE_ACTIVITY_REQUEST, str(activity.id))
      conn.expire(RedisKeynameConfig().CODE_ACTIVITY_REQUEST, 60)

  except Exception as e:
    res = ApiResponse(None, 'Internal Server Error', 'A0500', repr(e))
    return jsonify(res.to_dict()), 500

  res = ApiResponse(None, 'Success', 'A0200')
  return jsonify(res.to_dict()), 200
